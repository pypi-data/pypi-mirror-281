from deta import Deta
import os
import posixpath


class DetaPathLike(os.PathLike):
    """
    A class that implements the os.PathLike interface for working with Deta.Drive.
    It provides a file system-like interface for Deta.Drive operations.
    """

    def __init__(self, project_key, drive_name):
        """
        Initialize the DetaPathLike object.

        Args:
            project_key (str): The project key for Deta.
            drive_name (str): The name of the Deta.Drive to use.
        """
        self.deta = Deta(project_key)
        self.drive = self.deta.Drive(drive_name)
        self.base = self.deta.Base("detafs")
        self.drive_name = drive_name

    def __fspath__(self):
        """
        Return the file system path representation.

        Returns:
            str: A string representation of the path.
        """
        return f"deta://{self.drive_name}"

    def __str__(self):
        """
        Return a string representation of the DetaPathLike object.

        Returns:
            str: A string representation of the path.
        """
        return self.__fspath__()

    def __repr__(self):
        """
        Return a detailed string representation of the DetaPathLike object.

        Returns:
            str: A detailed string representation of the object.
        """
        return f"DetaPathLike('{self.drive_name}')"

    def _get_path_info(self, path):
        """
        Get information about a path from Deta.Base.

        Args:
            path (str): The path to get information about.

        Returns:
            dict: Information about the path, or None if it doesn't exist.
        """
        return self.base.get(f"{self.drive_name}:{path}")

    def _set_path_info(self, path, is_file=True):
        """
        Set information about a path in Deta.Base.

        Args:
            path (str): The path to set information for.
            is_file (bool): Whether the path is a file (True) or directory (False).
        """
        self.base.put({"path": path, "is_file": is_file}, f"{self.drive_name}:{path}")

    def _delete_path_info(self, path):
        """
        Delete information about a path from Deta.Base.

        Args:
            path (str): The path to delete information for.
        """
        self.base.delete(f"{self.drive_name}:{path}")

    def listdir(self, path=""):
        """
        List the contents of a directory.

        Args:
            path (str): The path of the directory to list. Defaults to root.

        Returns:
            list: A list of items in the directory.
        """
        items = self.base.fetch({"path?pfx": f"{self.drive_name}:{path}"})
        return [item["path"].split("/")[-1] for item in items.items]

    def is_file(self, path):
        """
        Check if a path is a file.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path is a file, False otherwise.
        """
        info = self._get_path_info(path)
        return info and info.get("is_file", False)

    def is_dir(self, path):
        """
        Check if a path is a directory.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path is a directory, False otherwise.
        """
        info = self._get_path_info(path)
        return info and not info.get("is_file", True)

    def exists(self, path):
        """
        Check if a path exists.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return self._get_path_info(path) is not None

    def mkdir(self, path, parents=False, exist_ok=False):
        """
        Create a directory.

        Args:
            path (str): The path of the directory to create.
            parents (bool): If True, create parent directories as needed.
            exist_ok (bool): If True, don't raise an error if the directory already exists.

        Raises:
            FileExistsError: If the directory already exists and exist_ok is False.
        """
        if self.exists(path):
            if exist_ok:
                return
            else:
                raise FileExistsError(f"Path already exists: {path}")
        if parents:
            parts = path.split("/")
            for i in range(1, len(parts) + 1):
                self._set_path_info("/".join(parts[:i]), is_file=False)
        else:
            self._set_path_info(path, is_file=False)

    def _remove_recursive(self, path):
        """
        Recursively remove a path and its contents.

        Args:
            path (str): The path to remove.
        """
        if self.is_file(path):
            self.drive.delete(path)
            self._delete_path_info(path)
        else:
            for item in self.listdir(path):
                item_path = self.join(path, item)
                self._remove_recursive(item_path)
            self._delete_path_info(path)

    def rmdir(self, path):
        """
        Remove a directory and all its contents.

        Args:
            path (str): The path of the directory to remove.

        Raises:
            NotADirectoryError: If the path is not a directory.
        """
        if not self.is_dir(path):
            raise NotADirectoryError(f"Not a directory: {path}")
        self._remove_recursive(path)

    def remove(self, path):
        """
        Remove a file or directory.

        Args:
            path (str): The path to remove.

        Raises:
            FileNotFoundError: If the path does not exist.
        """
        if not self.exists(path):
            raise FileNotFoundError(f"No such file or directory: {path}")
        self._remove_recursive(path)

    def open(self, path, mode="r"):
        """
        Open a file.

        Args:
            path (str): The path of the file to open.
            mode (str): The mode to open the file in ('r', 'rb', 'w', or 'wb').

        Returns:
            DetaFileReader or DetaFileWriter: An object for reading from or writing to the file.

        Raises:
            FileNotFoundError: If the file does not exist in read mode.
            ValueError: If an unsupported mode is specified.
        """
        if mode in ("r", "rb"):
            if not self.exists(path):
                raise FileNotFoundError(f"No such file: {path}")
            return DetaFileReader(self, path)
        elif mode in ("w", "wb"):
            return DetaFileWriter(self, path)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def join(self, *paths):
        """
        Join one or more path components.

        Args:
            *paths: Path components to join.

        Returns:
            str: The joined path.
        """
        return posixpath.join(*paths)

    def basename(self, path):
        """
        Return the base name of a path.

        Args:
            path (str): The path to get the base name of.

        Returns:
            str: The base name of the path.
        """
        return posixpath.basename(path)

    def dirname(self, path):
        """
        Return the directory name of a path.

        Args:
            path (str): The path to get the directory name of.

        Returns:
            str: The directory name of the path.
        """
        return posixpath.dirname(path)

    def iter(self, path, chunk_size=None):
        """
        Return an iterator for the contents of a file.

        Args:
            path (str): The path of the file to iterate over.
            chunk_size (int, optional): The size of each chunk to yield.

        Returns:
            iterator: An iterator yielding chunks of the file's contents.

        Raises:
            FileNotFoundError: If the file does not exist.
            IsADirectoryError: If the path is a directory.
        """
        if not self.exists(path):
            raise FileNotFoundError(f"No such file: {path}")
        if self.is_dir(path):
            raise IsADirectoryError(f"Is a directory: {path}")
        return self.drive.get(path).iter_chunks(chunk_size)


class DetaFileReader:
    """
    A class that provides a file-like interface for reading files from Deta.Drive.
    """

    def __init__(self, deta_path, path):
        """
        Initialize the DetaFileReader.

        Args:
            deta_path (DetaPathLike): The DetaPathLike object.
            path (str): The path of the file to read.
        """
        self.deta_path = deta_path
        self.path = path
        self._iterator = None

    def read(self, size=-1):
        """
        Read from the file.

        Args:
            size (int): The number of bytes to read. If -1, read the entire file.

        Returns:
            bytes: The read content.
        """
        if self._iterator is None:
            self._iterator = self.deta_path.iter(self.path)

        if size == -1:
            return b"".join(self._iterator)

        result = b""
        while len(result) < size:
            try:
                chunk = next(self._iterator)
                result += chunk[: size - len(result)]
            except StopIteration:
                break
        return result

    def __iter__(self):
        """
        Return an iterator for the file's contents.

        Returns:
            iterator: An iterator yielding chunks of the file's contents.
        """
        return self.deta_path.iter(self.path)

    def __enter__(self):
        """
        Enter the runtime context for the DetaFileReader.

        Returns:
            DetaFileReader: The DetaFileReader object.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context for the DetaFileReader.
        """
        pass


class DetaFileWriter:
    """
    A class that provides a file-like interface for writing files to Deta.Drive.
    """

    def __init__(self, deta_path, path):
        """
        Initialize the DetaFileWriter.

        Args:
            deta_path (DetaPathLike): The DetaPathLike object.
            path (str): The path of the file to write.
        """
        self.deta_path = deta_path
        self.path = path
        self.buffer = None

    def write(self, data):
        """
        Write data to the file.

        Args:
            data (bytes | str): The data to write.
        """
        self.buffer = data

    def close(self):
        """
        Close the file and write its contents to Deta.Drive.
        """
        self.deta_path.drive.put(self.path, self.buffer)
        self.deta_path._set_path_info(self.path)

    def __enter__(self):
        """
        Enter the runtime context for the DetaFileWriter.

        Returns:
            DetaFileWriter: The DetaFileWriter object.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context for the DetaFileWriter and close the file.
        """
        self.close()
